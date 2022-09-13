import { useEffect, useState } from "react";
import { BsGithub } from "react-icons/bs";
import ResourcesList from "./ResourcesList";
import ResourceViewer from "./ResourceViewer";
import SourcesList from "./SourcesList";
import Logo from "assets/idea.png";
import { HiMenu } from "react-icons/hi";
import { useResource } from "hooks/useResource";

const Layout = () => {
  const [openMenu, setOpenMenu] = useState(false);
  const { resource } = useResource();

  useEffect(() => {
    if (resource && window.innerWidth <= 640) {
      setOpenMenu(true);
    }
  }, [resource]);

  return (
    <div className="w-screen h-screen flex flex-col">
      <div className="bg-gray-800 text-gray-50 flex justify-between px-8 py-4">
        <div className="flex items-center">
          <HiMenu className="text-white text-2xl mr-4" onClick={() => setOpenMenu((menu) => !menu)} />
          <h1 className="text-xl">
            <img src={Logo} alt="Logo" className="w-8 h-8 inline-block mr-2" /> AI Book
          </h1>
        </div>
        <div className="flex space-x-4">
          <a href={`https://github.com/${import.meta.env.VITE_REPO}`} target="blank">
            <BsGithub className="text-2xl" title={import.meta.env.VITE_REPO} />
          </a>
        </div>
      </div>
      <div className="grow w-full overflow-hidden flex relative">
        <div className={"w-full sm:w-fit h-full flex items-stretch" + (openMenu ? " absolute -left-full" : " ")}>
          <SourcesList className="px-2 w-20 overflow-y-scroll shadow-2xl" />
          <ResourcesList className="px-4 grow w-full md:grow-0 md:w-96 overflow-y-scroll shadow-2xl" />
        </div>
        <ResourceViewer className={"sm:grow" + (openMenu ? " absolute top-0 w-screen h-screen" : " hidden sm:block")} />
      </div>
    </div>
  );
};

export default Layout;
