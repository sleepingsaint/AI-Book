import React, { useState } from "react";
import { ResourceType, SourceType } from "types";

export const ResourceContext = React.createContext<{
  source?: SourceType;
  setSource: React.Dispatch<React.SetStateAction<SourceType | undefined>>;
  resource?: ResourceType;
  setResource: React.Dispatch<React.SetStateAction<ResourceType | undefined>>;
}>({ setSource: () => {}, setResource: () => {} });

export const ResourceContextProvider: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => {
  const [source, setSource] = useState<SourceType>();
  const [resource, setResource] = useState<ResourceType>();

  return (
    <ResourceContext.Provider value={{ source, setSource, resource, setResource }}>{children}</ResourceContext.Provider>
  );
};
