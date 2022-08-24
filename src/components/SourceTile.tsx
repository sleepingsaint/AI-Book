import { useResource } from "hooks/useResource";
import { SourceType } from "types";

const SourceTile: React.FC<{ source: SourceType } & React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const {source, setSource} = useResource();
  const selectedStyle = source && source.source_id === props.source.source_id ? "bg-slate-200 p-2 rounded-xl" : " rounded";
  return (
    <img
      src={props.source.icon}
      className={"h-12 w-12 my-2 mb-4 mx-auto " + selectedStyle} 
      alt={props.source.title}
      title={props.source.title}
      {...props}
      onClick={() => setSource({...props.source})}
    />
  );
};

export default SourceTile;
