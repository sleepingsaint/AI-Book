import { useResource } from "hooks/useResource";
import React from "react";

const ResourceViewer: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const { resource } = useResource();

  if(!resource) return <div {...props}>Select a resource</div>
  return <iframe src={resource.url} frameBorder="0" {...props}></iframe>
};

export default ResourceViewer;
