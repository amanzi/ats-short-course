(setq inhibit-startup-screen t)
(setq visible-bell nil)
(setq ring-bell-function 'ignore)

;; MELPA packages
(require 'package)
(add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/"))
(package-initialize)
(require 'use-package)


;; fancy html jump
(require 'sgml-mode)
(autoload 'sgml-skip-tag-backward "sgml-mode" nil t)
(autoload 'sgml-skip-tag-forward "sgml-mode" nil t)
(defun html-get-tag ()
  (let ((b (line-beginning-position))
        (e (line-end-position))
        (looping t)
        (html-tag-char (string-to-char "<"))
        (char (following-char))
        (p (point))
        (found_tag -1))

    (save-excursion
      ;; search backward
      (unless (= char html-tag-char)
        (while (and looping (<= b (point)) (not (= char 60)))
          (setq char (following-char))
          (setq p (point))
          (if (= p (point-min))
              ;; need get out of loop anyway
              (setq looping nil)
            (backward-char))))

      ;; search forward
      (if (not (= char html-tag-char))
          (save-excursion
            (while (and (>= e (point)) (not (= char 60)))
              (setq char (following-char))
              (setq p (point))
              (forward-char))))

      ;; is end tag?
      (when (and (= char html-tag-char) (< p e))
        (goto-char p)
        (forward-char)
        (if (= (following-char) 47)
            (progn
              ;; </
              (skip-chars-forward "^>")
              (forward-char)
              (setq p (point))
              (setq found_tag 1))
          (progn
            ;; < , looks fine
            (backward-char)
            (setq found_tag 0)))))
    found_tag))



;;
;; xml
;;
(require 'hideshow)
(require 'nxml-mode)

(defun html-jump(&optional num)
  "Jump forward from html open tag"
  (interactive "P")
  (unless num (setq num 1))
  ;; web-mode-forward-sexp is assigned to forward-sexp-function
  ;; it's buggy in web-mode v11, here is the workaround
  (let ((backup-forward-sexp-function forward-sexp-function))
    (if (= (html-get-tag) 0)
        (sgml-skip-tag-forward num)
      (sgml-skip-tag-backward num))))

(add-to-list 'hs-special-modes-alist
             '(nxml-mode
               "<!--\\|<[^/>]*[^/]>"
               "-->\\|</[^/>]*[^/]>"

               "<!--"
               sgml-skip-tag-forward
               nil))
(add-hook 'nxml-mode-hook 'hs-minor-mode)


(defun my-xml-mode-keys ()
  "my keys for `xml-mode'."
  (interactive)
  (local-set-key (kbd "M-;") 'html-jump)
  (local-set-key (kbd "C-;") 'hs-toggle-hiding)
  )

(use-package nxml-mode
  :mode (("\\.xml$" . nxml-mode)
         ("\\.zcml$" . nxml-mode)
         ("\\.xmf$" . nxml-mode))
  :config
  (add-hook 'nxml-mode-hook 'my-xml-mode-keys))

(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(font-lock-string-face ((t (:foreground "DarkOrchid3"))))
 '(nxml-attribute-local-name ((t (:foreground "black"))))
 '(nxml-element-local-name ((t (:foreground "dark gray"))))
 )

