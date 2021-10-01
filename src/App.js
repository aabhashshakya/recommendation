import { useState, useEffect } from "react";

function App() {
  const [bookList, setBookList] = useState(null);

  // useEffect(() => {
  //   fetch("/msg")
  //     .then((res) => res.json())
  //     .then((data) => console.log(data.hello));
  // }, []);

  useEffect(() => {
    fetch("/getbooklist")
      .then((res) => {
        console.log(res);
        return res.json();
      })
      .then((data) => {
        console.log(data);
        const result = Object.values(data);
        // console.log(result);
        // result.map((re) => console.log(re));
        setBookList(result);

        // setBookList(data);
      });
  }, []);

  console.log(bookList);
  return (
    <div className="App">
      {bookList ? (
        <div>
          <h1>LIST OF BOOK </h1>
          {/* {bookList[0]["Book-Title"]} */}
          {bookList.map((book) => (
            <h1>{book["Book-Title"]}</h1>
          ))}
        </div>
      ) : (
        <h1>no books</h1>
      )}
    </div>
  );
}

export default App;
