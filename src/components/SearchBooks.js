import React, { useState } from "react";

function SearchBooks() {
  const [title, setTitle] = useState("");
  return (
    <div className="searchbook">
      <div className="search-form">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetch("/searchbook", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                content: title,
              }),
            })
              .then((res) => res.json())
              .then((message) => {
                console.log(message);
                setTitle("");
              });
          }}
        >
          <input
            onChange={(e) => setTitle(e.target.value)}
            type="text"
            placeholder="Title..."
            required
            value={title}
          />
          <button className="search-button">Add Book</button>
        </form>
        {title ? <h1>{title}</h1> : <h1>empty</h1>}
      </div>
    </div>
  );
}

export default SearchBooks;
