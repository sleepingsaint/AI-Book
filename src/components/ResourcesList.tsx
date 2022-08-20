import { useResource } from "hooks/useResource";
import React, { Fragment, useCallback } from "react";
import { useInfiniteQuery } from "react-query";
import { ResourceType } from "types";
import ResourceTile from "./ResourceTile";
import { FiDownload, FiLoader, FiExternalLink } from "react-icons/fi";
import SelectSourceSVG from 'assets/select_source.svg';
import {MdOutlineErrorOutline} from 'react-icons/md';

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

  const { data, isLoading, isError, hasNextPage, fetchNextPage, isFetching, isFetchingNextPage, refetch } = useInfiniteQuery<
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
    return <div {...props}>
      <div className="w-full h-full flex flex-col justify-center items-center">
        <img src={SelectSourceSVG} className="w-2/3" alt="select source" />
        <p className="mt-4">Select a source</p>
      </div>
    </div>;
  }
  if (isError) return <div {...props}>
    <div className="w-full h-full flex flex-col justify-center items-center ">
      <p><MdOutlineErrorOutline className="text-red-300 text-2xl font-bold inline-block mr-2" /> Oops! something went wrong</p>
      <button onClick={() => refetch()}>Retry</button>
    </div>
</div>;
  if (isLoading) return <div {...props}>
    <div className="w-full h-full flex flex-col justify-center items-center">
      <p><FiLoader className="inline-block mr-2" /> Loading</p>
    </div>
  </div>;

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
