import { ResourceType } from "types"
import {FiUsers} from 'react-icons/fi';
import {AiOutlineTags} from 'react-icons/ai'
import {MdDateRange} from 'react-icons/md';
import { useResource } from "hooks/useResource";

const ResourceTile: React.FC<{resource: ResourceType}> = ({resource}) => {
  const {resource: res, setResource} = useResource();
  const selectedStyle = res && res.resource_db_id === resource.resource_db_id ? " bg-blue-100": "";
  return (
    <div className={"p-2 shadow-md my-2 cursor-pointer" + selectedStyle} onClick={() => setResource({...resource})}>
      <p className="mb-2 font-bold">{resource.title}</p>
      {resource.authors && <p className="truncate" title={resource.authors}><FiUsers className="inline-block mr-2"/> {resource.authors}</p>}
      {resource.tags && <p className="truncate" title={resource.tags}><AiOutlineTags className="inline-block mr-2"/> {resource.tags}</p>}
      {resource.publishedOn && <p><MdDateRange className="inline-block mr-2"/> {(new Date(resource.publishedOn)).toDateString()}</p>}
    </div>
  )
}

export default ResourceTile
