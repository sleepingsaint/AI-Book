import { useResource } from "hooks/useResource";
import React, { useEffect } from "react";
import SelectResourceSVG from "assets/select_resource.svg";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const ResourceViewer: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const { resource } = useResource();

  const truncateString = (str: string) => {
    const len = 100;
    if (str.length > len) {
      return `Loading '${str.substring(0, len)}'...`;
    }
    return `Loading '${str}'`;
  };

  useEffect(() => {
    toast.dismiss();
    if (resource) {
      toast.info(truncateString(resource.title));
    }
  }, [resource]);

  if (!resource) {
    return (
      <div {...props}>
        <div className="w-full h-full flex flex-col justify-center items-center">
          <img src={SelectResourceSVG} className="lg:w-1/3 w-2/3" alt="select resource" />
          <p className="mt-8 text-xl">Select a Resource</p>
        </div>
      </div>
    );
  }

  return (
    <div className={props.className + " relative"}>
      <ToastContainer
        position="top-right"
        autoClose={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable={false}
        theme="colored"
      />
      <iframe src={resource.url} onLoad={() => toast.dismiss()} frameBorder="0" className="w-full h-full"></iframe>;
    </div>
  );
};

export default ResourceViewer;
