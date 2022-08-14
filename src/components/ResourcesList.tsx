import { Fragment, useState } from "react";
import { useQuery, useInfiniteQuery } from "react-query";
import { ResourceType } from "types";
import ResourceTile from "./ResourceTile";

const fetchResources = async ({ pageParam = 0 }) => {
  const endpoint = `https://raw.githubusercontent.com/sleepingsaint/resource_scrapper_test/db/resources/googleaiblog/${pageParam}.json`;
  const resp = await fetch(endpoint);
  return resp.json();
};

const ResourcesList = () => {
  const [resourceURL, setResourceURL] = useState<string>();

  const {
    data,
    isLoading,
    isError,
    hasNextPage,
    fetchNextPage,
    isFetching,
    isFetchingNextPage,
  } = useInfiniteQuery<ResourceType[]>("getResources", fetchResources, {
    getNextPageParam: (lastPage, pages) => {
      if (pages.length < 37) {
        return pages.length + 1;
      }
      return undefined;
    },
  });

  if (isError) return <div>Oops something went wrong</div>;
  if (isLoading) return <div> Loading ...</div>;

  return (
    <div style={{display: "flex", width: "100vw", height: "100vh"}}>
      <div style={{width: "30%", height: "100vh", overflow: "hidden", overflowY: "scroll"}}>
      {data &&
        data.pages &&
        data.pages.map((group, idx) => (
          <Fragment key={idx}>
            {group.map((res) => (
              <p onClick={() => setResourceURL(res.url)} style={{cursor: "pointer"}}>
                <ResourceTile resource={res} key={res.resource_db_id} />
              </p>
            ))}
          </Fragment>
        ))}
      {isFetching && isFetchingNextPage && <div>Loading More resources</div>}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()}>Load More</button>
        )}
        </div>
        <div style={{height: "100vh", overflow: "hidden", overflowY: "scroll", width: "100%"}}>
          {resourceURL ? <iframe src={resourceURL.replace("http", "https")} style={{width: "100%", height: "100%"}}/> : <p>No resource selected</p>}
        </div>
    </div>
  );
};

export default ResourcesList;
