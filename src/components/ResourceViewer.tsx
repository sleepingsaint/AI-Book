import { useResource } from "hooks/useResource";
import React, { useState, useEffect } from "react";
import SelectResourceSVG from "assets/select_resource.svg";
import { FiLoader } from "react-icons/fi";

const ResourceViewer: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const { resource } = useResource();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (resource) {
      setLoading(true);
    }
  }, [resource]);

  if (!resource)
    return (
      <div {...props}>
        <div className="w-full h-full flex flex-col justify-center items-center">
          <img src={SelectResourceSVG} className="lg:w-1/3 w-2/3" alt="select resource" />
          <p className="mt-8 text-xl">Select a Resource</p>
        </div>
      </div>
    );

  return (
    <div className={props.className + " relative"}>
      {loading && (
        <div className="w-full h-full bg-slate-50/75 flex justify-center items-center absolute">
          <FiLoader className="text-xl mr-2" /> loading
        </div>
      )}
      <iframe src={resource.url} onLoad={(e) => setLoading(false)} frameBorder="0" className="w-full h-full"></iframe>;
    </div>
  );
};

export default ResourceViewer;
