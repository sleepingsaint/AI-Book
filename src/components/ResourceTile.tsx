import { ResourceType } from "types"

const ResourceTile: React.FC<{resource: ResourceType}> = ({resource}) => {
  return (
    <div>{resource.title}</div>
  )
}

export default ResourceTile