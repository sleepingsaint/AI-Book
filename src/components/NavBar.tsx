import { BsGithub } from "react-icons/bs";
import Logo from 'assets/idea.png';

const NavBar = () => {
  return (
    <div className="bg-gray-800 text-gray-50 flex justify-between px-8 py-4">
      <h1 className="text-2xl"><img src={Logo} alt="Logo" className="w-8 h-8 inline-block mr-2" /> Resource Scrapper</h1>
      <div className="flex space-x-4">
        <a href={`https://github.com/${import.meta.env.VITE_REPO}`} target="blank">
          <BsGithub className="text-2xl" title={import.meta.env.VITE_REPO} />
        </a>
      </div>
    </div>
  );
};

export default NavBar;
