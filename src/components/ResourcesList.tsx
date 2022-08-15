import { useResource } from "hooks/useResource";
import React, { Fragment, useCallback } from "react";
import { useInfiniteQuery } from "react-query";
import { ResourceType } from "types";
import ResourceTile from "./ResourceTile";
import { FiDownload, FiLoader, FiExternalLink } from "react-icons/fi";

// const fetchResources = async ({ pageParam = 0 }) => {
//   const endpoint = `https://raw.githubusercontent.com/sleepingsaint/resource_scrapper_test/db/resources/googleaiblog/${pageParam}.json`;
//   const resp = await fetch(endpoint);
//   return resp.json();
// };

const ResourcesList: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
  const { source } = useResource();
  const fetchResources = useCallback(
    async ({ pageParam = 0 }) => {
      if (source) {
        const endpoint = `https://raw.githubusercontent.com/sleepingsaint/resource_scrapper_test/db/resources/${source.source_id}/${pageParam}.json`;
        const resp = await fetch(endpoint);
        return resp.json();
      }
      return () => [];
    },
    [source]
  );

  const { data, isLoading, isError, hasNextPage, fetchNextPage, isFetching, isFetchingNextPage } = useInfiniteQuery<
    ResourceType[]
  >("getResources", fetchResources, {
    getNextPageParam: (lastPage, pages) => {
      if (pages.length < 37) {
        return pages.length;
      }
      return undefined;
    },
    enabled: source !== undefined,
  });

  if (!source) {
    return <div {...props}>Select source</div>;
  }
  if (isError) return <div>Oops something went wrong</div>;
  if (isLoading) return <div> Loading ...</div>;

  return (
    <div {...props}>
      <div className="my-2 py-4">
        <h3 className="text-2xl relative">
          {source.title}
          <span className="text-xs absolute top-[-10] bg-blue-200 p-0.5 rounded">{source.num_resources}</span>
          <a href={source.url} target="blank" className="inline-block float-right">
            <FiExternalLink />
          </a>
        </h3>
        <hr className="mt-2" />
      </div>
      {data &&
        data.pages &&
        data.pages.map((group, idx) => (
          <Fragment key={idx}>
            {group.map((res) => (
              <ResourceTile resource={res} key={res.resource_db_id} />
            ))}
          </Fragment>
        ))}

      {isFetching && isFetchingNextPage && (
        <div className="w-full p-2 bg-blue-400 my-4 rounded-md text-white text-center">
          <FiLoader className="inline-block mr-2" /> Loading More Resources
        </div>
      )}
      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          className="w-full p-2 bg-blue-800 my-4 rounded-md text-white text-center"
          disabled={isFetching || isFetchingNextPage}
        >
          <FiDownload className="inline-block mr-2" /> Load More
        </button>
      )}
    </div>
  );
};

export default ResourcesList;
