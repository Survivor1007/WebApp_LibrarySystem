import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

type Book = {
  id: number;
  title: string;
  author: string;
  available_copies: number;
};

const Books = () => {
  const { access, refresh, login, logout } = useAuth();
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        let token = access;

        let res = await fetch("http://127.0.0.1:8000/api/books/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Bearer ${token}` : "",
          },
        });

        // If access expired -> try refresh
        if (res.status === 401 && refresh) {
          const refreshRes = await fetch(
            "http://127.0.0.1:8000/api/token/refresh/",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ refresh }),
            }
          );

          if (refreshRes.ok) {
            const data = await refreshRes.json();
            token = data.access;

            // update context + storage
            //login(token, refresh,null);

            // retry books fetch with new token
            res = await fetch("http://127.0.0.1:8000/api/books/", {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            });
          } else {
            logout();
            navigate("/login");
            return;
          }
        }

        if (!res.ok) throw new Error("Failed to fetch books");

        const data = await res.json();
        setBooks(data);
      } catch (err) {
        setError("Could not load books.");
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, [access, refresh, login, logout, navigate]);

  if (loading) return <p className="text-center mt-6">Loading books...</p>;
  if (error) return <p className="text-center text-red-500 mt-6">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-green-600">Available Books</h1>
      {books.length === 0 ? (
        <p className="text-gray-600">No books available right now.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {books.map((book) => (
            <div
              key={book.id}
              className="bg-white shadow-md rounded-2xl p-4 border border-gray-200"
            >
              <h2 className="text-lg font-semibold">{book.title}</h2>
              <p className="text-gray-600">Author: {book.author}</p>
              <p className="text-gray-600">
                Copies Available: {book.available_copies}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Books;
