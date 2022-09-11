import { ResourceType } from "types";
import { FiUsers } from "react-icons/fi";
import { AiOutlineTags } from "react-icons/ai";
import { MdDateRange } from "react-icons/md";
import { useResource } from "hooks/useResource";
import { FiExternalLink } from "react-icons/fi";

const ResourceTile: React.FC<{ resource: ResourceType }> = ({ resource }) => {
  const { resource: res, setResource } = useResource();
  const selectedStyle = res && res.resource_db_id === resource.resource_db_id ? " bg-blue-100" : "";
  return (
    <div
      className={"group p-2 shadow-md my-2 cursor-pointer" + selectedStyle}
      onClick={() => setResource({ ...resource })}
    >
      <p className="mb-2 font-bold">{resource.title}</p>
      {resource.authors && (
        <p className="truncate" title={resource.authors}>
          <FiUsers className="inline-block mr-2" /> {resource.authors}
        </p>
      )}
      {resource.tags && (
        <p className="truncate" title={resource.tags}>
          <AiOutlineTags className="inline-block mr-2" /> {resource.tags}
        </p>
      )}
      {resource.publishedOn && (
        <p className="flex justify-between mt-1">
          <div>
            <MdDateRange className="inline-block mr-2" /> {new Date(resource.publishedOn).toDateString()}
          </div>
          <a className="hidden group-hover:inline mr-2 bg-blue-200 px-2" target="_blank" href={resource.url}>
            <FiExternalLink className="inline mr-1" />
            <span>Open</span>
          </a>
        </p>
      )}
    </div>
  );
};

export default ResourceTile;