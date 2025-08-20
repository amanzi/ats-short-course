# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: all sphinx_help worktree html pdf deploy clean

all: html

help:
	@echo "Builds short course public website
	@echo "---------------------------------------"
	@echo "To build documentation from scratch (new repo setup, do this once):"
	@echo "  > make worktree"
	@echo ""
	@echo "To build website:"
	@echo "  > make"
	@echo ""
	@echo "To deploy to github:"
	@echo "  > make deploy"

sphinx_help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

worktree:
	cd deploy && git worktree add html gh-pages

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


deploy:
	mkdir -p deploy/html/`git branch --show-current`
	cp -r build/html/* deploy/html/`git branch --show-current`/
	cd deploy/html && \
	git add --all && \
	git commit -m "Deployment to gh-pages" && \
	git push origin gh-pages

clean:
	rm -rf build/html


