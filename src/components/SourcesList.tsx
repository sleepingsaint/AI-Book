import React, { Fragment } from "react";
import { useQuery } from "react-query";
import { SourceType } from "types";
import SourceTile from "./SourceTile";

const getSources = async ({ pageParam = 0 }) => {
  const resp = await fetch(
    `https://raw.githubusercontent.com/${import.meta.env.VITE_REPO}/db/sources/${pageParam}.json`
  );
  return resp.json();
};

const SourcesList: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const {data, isError, isLoading, error} = useQuery<SourceType[]>("getSources", getSources)
  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Oops! something went wrong</div>;

  return (
    <div {...props}>
      {data && data.map(src => <SourceTile source={src} key={src.source_db_id} />)}
    </div>
  );
};

export default SourcesList;
