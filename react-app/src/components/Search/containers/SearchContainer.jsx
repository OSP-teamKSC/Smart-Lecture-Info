import React from "react";
import SearchBar from "../SearchBar";
import SearchSelect from "../SearchSelect";

const SearchContainer = () => {
    return <div className="search-wrap">
        <SearchSelect/>
        <SearchBar/>
    </div>;
}

export default SearchContainer;