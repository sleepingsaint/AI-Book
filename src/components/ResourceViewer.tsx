import { useResource } from "hooks/useResource";
import React from "react";
import SelectResourceSVG from "assets/select_resource.svg";

const ResourceViewer: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const { resource } = useResource();

  if (!resource)
    return (
      <div {...props}>
        <div className="w-full h-full flex flex-col justify-center items-center">
          <img src={SelectResourceSVG} className="lg:w-1/3 w-2/3" alt="select resource" />
          <p className="mt-8 text-xl">Select a Resource</p>
        </div>
      </div>
    );

  return <iframe src={resource.url} frameBorder="0" {...props}></iframe>;
};

export default ResourceViewer;
