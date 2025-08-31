import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div className="flex h-screen flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-red-600">404 - Page Not Found</h1>
      <Link
        to="/"
        className="mt-4 text-blue-600 underline hover:text-blue-800"
      >
        Go Home
      </Link>
    </div>
  );
};

export default NotFound;
