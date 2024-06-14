import React, { useState } from "react";
import axios from "axios";

const AddHistoricalEntryForm = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [year, setYear] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();

        const token = localStorage.getItem("token");
        const refreshToken = localStorage.getItem("refreshToken");

        axios
            .post(
                `${backendUrl}/historical_entries`,
                {
                    title: title,
                    description: description,
                    year: year
                },
                {
                    headers: {
                        Authorization: "Bearer " + token,
                        refresh_token: refreshToken,
                    },
                }
            )
            .then((response) => {
                console.log("Historical entry added successfully");
                setTitle("");
                setDescription("");
                setYear("");
                window.location.reload(); // Consider updating the list without reloading the page
            })
            .catch((error) => {
                console.error("Error adding historical entry: ", error);
            });
    };

    return (
        <div>
            <h2>Add Historical Entry</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(event) => setTitle(event.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Description:</label>
                    <textarea
                        value={description}
                        onChange={(event) => setDescription(event.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Year:</label>
                    <input
                        type="number"
                        value={year}
                        onChange={(event) => setYear(event.target.value)}
                        required
                    />
                </div>
                <button type="submit">Add Entry</button>
            </form>
        </div>
    );
};

export default AddHistoricalEntryForm;