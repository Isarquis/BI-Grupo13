import { Link } from "react-router-dom";

export default function Home() {
    return (
      <div className="p-4 max-w-lg mx-auto text-center">
        <h1 className="text-xl font-bold mb-4">Clasificador de Noticias</h1>
        <Link to="/predict" className="bg-blue-500 text-white p-2 rounded mr-2">
          Predecir Noticias
        </Link>
        <Link to="/otro" className="bg-gray-500 text-white p-2 rounded">
          Otro Endpoint
        </Link>
      </div>
    );
  }