import React from "react"
import { ResourceContext } from "contexts/ResourceContext"

export const useResource = () => {
    return React.useContext(ResourceContext);
}