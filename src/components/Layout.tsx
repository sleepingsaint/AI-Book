import NavBar from "./NavBar"
import ResourcesList from "./ResourcesList"
import ResourceViewer from "./ResourceViewer"
import SourcesList from "./SourcesList"

const Layout = () => {
  return (
    <div className="h-screen w-screen flex flex-col">
        <NavBar />
        <div className="grow flex">
          <SourcesList className="w-20 shadow-xl"/>
          {/* <ResourcesList className="px-4 w-96 box-content h-full shadow-lg overflow-hidden overflow-y-scroll"/> */}
          <ResourcesList className="w-96 px-4 box-content h-full shadow-lg overflow-hidden overflow-y-scroll"/>
          <ResourceViewer className="grow px-2 flex flex-col justify-center items-center"/>
        </div>
    </div>
  )
}

export default Layout