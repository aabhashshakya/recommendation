import { useState, useEffect } from "react";

function App() {
  const [bookList, setBookList] = useState("");

  useEffect(() => {
    fetch("/msg")
      .then((res) => res.json())
      .then((data) => console.log(data.hello));
  }, []);
  return <div className="App"></div>;
}

export default App;
