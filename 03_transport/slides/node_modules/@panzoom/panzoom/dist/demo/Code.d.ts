import 'prismjs/themes/prism-tomorrow.css';
import React from 'react';
interface Props {
    language?: string;
    children: string;
}
export default function Code({ children, language }: Props): React.JSX.Element;
export {};
