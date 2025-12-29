import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '@site/src/components/ChatWidget';

type LayoutProps = {
  children: React.ReactNode;
};

export default function Layout(props: LayoutProps): JSX.Element {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatWidget />
    </>
  );
}