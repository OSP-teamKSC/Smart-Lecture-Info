import React from "react";
import SearchContainer from "../Search/containers/SearchContainer";
import ViewContainer from "../View/containers/ViewContainer";

const Main = () => {
    return (
        <div className="main-wrap">
            <SearchContainer/>
            <ViewContainer/>
        </div>
    );
}

export default Main;