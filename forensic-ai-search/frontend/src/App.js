import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [count, setCount] = useState(0);

  const handleSearch = async () => {
    const response = await fetch("http://127.0.0.1:5000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    setResults(data.results);
    setCount(data.count);
  };

  const getColor = (risk) => {
    if (risk === "HIGH") return "#ef4444";
    if (risk === "MEDIUM") return "#f59e0b";
    return "#22c55e";
  };

  return (
    <div style={{ padding: "25px", fontFamily: "Arial", background: "#0f172a", minHeight: "100vh", color: "white" }}>
      
      <h1>AI Digital Forensic Investigation System</h1>

      <p style={{ color: "#94a3b8" }}>
        Semantic Keyword Search using NLP (Sentence Transformers)
      </p>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter forensic query..."
        style={{
          padding: "10px",
          width: "300px",
          borderRadius: "6px",
          border: "none"
        }}
      />

      <button
        onClick={handleSearch}
        style={{
          marginLeft: "10px",
          padding: "10px 15px",
          background: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer"
        }}
      >
        Search
      </button>

      <p style={{ marginTop: "15px", color: "#94a3b8" }}>
        Results found: {count}
      </p>

      <div style={{ marginTop: "20px" }}>
        {results.map((item, index) => (
          <div
            key={index}
            style={{
              background: "#1e293b",
              padding: "15px",
              marginBottom: "12px",
              borderRadius: "10px",
              borderLeft: `6px solid ${getColor(item.risk)}`
            }}
          >
            <p><b>Evidence:</b> {" "}
              {item.explanation.map((token, idx) => {
                let colour = "transparent";
                let text = "white";

                if (token.importance >= 0.45)
                {
                  colour = "#ef4444";
                }
                else if (token.importance >= 0.30)
                {
                  colour = "#f59e0b";
                }
                else if  (token.importance > 0)
                {
                  colour = "#22c55e"
                }

                return (
                  <span
                    key={idx}
                    style={{
                      backgroundColor: colour,
                      color: text,
                      padding: "2px 5px",
                      marginRight: "4px",
                      borderRadius: "4px",
                      fontWeight: token.importance > 0.2 ? "bold" : "normal"
                    }}
                  >
                    {token.word}
                  </span>
                );
              })}
            </p>

            <p>
              <b>Similarity Score:</b> {(item.score * 100).toFixed(2)}%
            </p>

            <p>
              <b>Risk Level:</b>{" "}
              <span style={{ color: getColor(item.risk), fontWeight: "bold" }}>
                {item.risk}
              </span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;