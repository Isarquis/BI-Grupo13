import { useState } from "react";

export default function NewsPredictor() {
  const [news, setNews] = useState([{ title: "", description: "" }]);
  const [predictions, setPredictions] = useState([]);

  const handleChange = (index, field, value) => {
    const updatedNews = [...news];
    updatedNews[index][field] = value;
    setNews(updatedNews);
  };

  const addNews = () => {
    setNews([...news, { title: "", description: "" }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await fetch("http://127.0.0.1:8000/predict/", {  // 🔴 Asegúrate de que el backend está en este puerto
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                titulo: news.map(n => n.title), 
                descripcion: news.map(n => n.description) 
            }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const result = await response.json();
        console.log("Respuesta del servidor:", result);
        setPredictions(result);  // Guardar la predicción en el estado
    } catch (error) {
        console.error("Error en la predicción:", error);
        alert("Error al conectar con el servidor.");
    }
};
  

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">Clasificador de Noticias Falsas</h1>
      <form onSubmit={handleSubmit}>
        {news.map((item, index) => (
          <div key={index} className="mb-3">
            <input
              type="text"
              placeholder="Título"
              value={item.title}
              onChange={(e) => handleChange(index, "title", e.target.value)}
              className="border p-2 w-full mb-2"
            />
            <textarea
              placeholder="Descripción"
              value={item.description}
              onChange={(e) => handleChange(index, "description", e.target.value)}
              className="border p-2 w-full"
            />
          </div>
        ))}
        <button type="button" onClick={addNews} className="bg-gray-200 p-2 rounded mr-2">
          Agregar Noticia
        </button>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Predecir
        </button>
      </form>
      {predictions.length > 0 && (
        <div className="mt-4">
          <h2 className="text-lg font-semibold">Resultados</h2>
          <ul>
            {predictions.map((pred, index) => (
              <li key={index} className="border p-2 mt-2">
                <strong>{pred.titulo}</strong>: {Math.round(pred.probabilidad * 100)}% verdadera
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
