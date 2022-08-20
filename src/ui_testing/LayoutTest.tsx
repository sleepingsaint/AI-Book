import NavBar from "components/NavBar";
import { useState } from "react";

const ListFC = () => {
  return (
    <div>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello</li>
      <li>Hello World</li>
    </div>
  );
};
const LayoutTest: React.FC<{}> = () => {
  const [source, setSource] = useState(false);
  const [resource, setResource] = useState(false);
  const [item, setItem] = useState(false);

  return (
    <div className="w-screen h-screen flex flex-col">
      <NavBar />
      <div className="grow w-full overflow-hidden flex relative bg-slate-50">
          <div className={"h-full flex items-stretch w-full sm:w-fit" + (item ? " absolute -left-full": " ")}>
            <div className="w-16 bg-slate-300">sources</div>
            <div className="grow w-full sm:grow-0 sm:w-64 bg-slate-400">Resources</div>
          </div>
          <div className={"bg-slate-500 sm:grow" + (item ? " absolute top-0 w-screen h-screen": " hidden sm:block")}> 
            hello
          </div>
          {/* <div className="bg-slate-200 h-full sm:w-auto flex items-stretch transition-all duration-500">
            <div className="bg-slate-300 h-full w-16 overflow-y-scroll"></div>
            <div className="bg-slate-400 grow sm:w-64 md:grow-0 overflow-y-scroll"></div>
          </div>
          <div>hell0</div> */}
      </div>
      {/* <div className="grow w-full bg-yellow-200 flex items-stretch overflow-hidden relative">
        <div className={"bg-slate-200 w-full sm:w-auto flex items-stretch transition-all duration-500"}>
          <div className="bg-slate-400 w-16 overflow-y-scroll"></div>
          <div className="bg-slate-500 grow sm:w-64 md:grow-0 overflow-y-scroll">
          </div>
        </div>
        <div>
          <button onClick={() => setItem(true)}>Click</button>
        </div>
      </div> */}
      {/* <div
        className={
          "w-full h-full bg-slate-500 transition-all overflow-auto duration-500" +
          (item ? " -left-full" : " left-0")
        }
      >
        <button onClick={() => setItem(true)} className="absolute">
          Resource
        </button>
        <div className="bg-yellow-200 h-full absolute overflow-y-scroll">
          <ListFC />
        </div>
      </div>
      <div
        className={
          "w-full h-full bg-slate-200 z-10 transition-all duration-500 absolute" + (item ? " left-0" : " left-full")
        }
      >
        <button onClick={() => setItem(false)}>IFrame</button>
      </div> */}
      {/* <div className={"absolute h-full w-full bg-slate-200 flex items-stretch transition-all duration-500" + (item ? " -translate-x-full": " translate-x-0")}>
        <div className={"bg-slate-300 relative" + (source ? " w-full": " w-16")}>
          {source && <button onClick={() => setSource(false)} className="absolute right-0">Close</button>}
          {!source && <button onClick={() => setSource(true)} className="absolute bottom-0">Expand</button>}
        </div>
        <div className="bg-slate-400 grow sm:grow-0">
          <button onClick={() => setItem(true)}>Resource</button>
        </div>
      <div className={"absolute bg-yellow-300 h-full sm:w-screen"}>
        <button onClick={() => setItem(false)}>URL asd;lkfjalskdjf;klajsdf</button>
      </div> */}
      {/* <div className="bg-slate-500 md:grow"></div> */}
      {/* </div> */}
    </div>
  );
};

export default LayoutTest;
