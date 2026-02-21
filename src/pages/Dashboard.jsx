import { useEffect, useState } from "react";
import API from "../api";

export default function Dashboard({ setPage }) {
  const [pets, setPets] = useState([]);
  const [name, setName] = useState("");
  const [breed, setBreed] = useState("");
  const [age, setAge] = useState("");
  const [weight, setWeight] = useState("");
  const [history, setHistory] = useState([]);

  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  const fetchPets = async () => {
    const res = await API.get("/pets/list");
    setPets(res.data);
  };

  useEffect(() => {
    fetchPets();
  }, []);

  const addPet = async () => {
    await API.post("/pets/add", null, {
      params: { name, breed, age, weight },
    });
    fetchPets();
  };

  const generateDiet = async (public_pet_id) => {
    await API.post(`/diet/generate/${public_pet_id}`);
    alert("Diet Generated!");
  };

  const getHistory = async (public_pet_id) => {
    const res = await API.get(`/diet/history/${public_pet_id}`);
    setHistory(res.data);
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Dashboard</h2>
      <button onClick={logout}>Logout</button>

      <hr />

      <h3>Add Pet</h3>
      <input placeholder="Name" onChange={(e) => setName(e.target.value)} />
      <input placeholder="Breed" onChange={(e) => setBreed(e.target.value)} />
      <input placeholder="Age" onChange={(e) => setAge(e.target.value)} />
      <input placeholder="Weight" onChange={(e) => setWeight(e.target.value)} />
      <button onClick={addPet}>Add Pet</button>

      <hr />

      <h3>Your Pets</h3>
      {pets.map((pet) => (
        <div key={pet.id} style={{ border: "1px solid gray", padding: 10, margin: 10 }}>
          <p><b>{pet.name}</b> ({pet.breed})</p>
          <p>Public ID: {pet.public_pet_id}</p>

          <button onClick={() => generateDiet(pet.public_pet_id)}>
            Generate Diet
          </button>

          <button onClick={() => getHistory(pet.public_pet_id)}>
            View History
          </button>
        </div>
      ))}

      <hr />

      <h3>Diet History</h3>
      {history.map((plan) => (
        <div key={plan.id} style={{ border: "1px solid blue", padding: 10, margin: 10 }}>
          <p><b>Date:</b> {plan.created_at}</p>
          <pre style={{ maxHeight: 200, overflow: "auto" }}>
            {JSON.stringify(plan.plan_data, null, 2)}
          </pre>
        </div>
      ))}
    </div>
  );
}