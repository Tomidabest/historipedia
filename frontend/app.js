import React, { useState, useEffect } from "react";
import AddHistoricalEntryForm from "./components/AddHistoricalEntryForm";
import HistoricalEntryList from "./components/HistoricalEntryList";
import Keycloak from "keycloak-js";

const keycloakConfig = {
    url: "http://localhost:8080/",
    realm: "historipediaRealm",
    clientId: "historipediaClient",
};
const keycloak = new Keycloak(keycloakConfig);

async function authenticateKeycloak() {
    try {
        const authenticated = await keycloak.init({
            onLoad: "login-required",
            checkLoginIframe: true,
        });
        if (authenticated) {
            console.log("User is authenticated");
            localStorage.setItem("token", keycloak.token);
            localStorage.setItem("refreshToken", keycloak.refreshToken);
            keycloak.onTokenExpired = () => {
                console.log("Token expired");
            };
            return true;
        } else {
            console.log("User is not authenticated");
            window.location.reload();
            return false;
        }
    } catch (error) {
        console.error("Authentication failed:", error);
        return false;
    }
}

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        authenticateKeycloak().then((authStatus) => {
            setIsAuthenticated(authStatus);
            setIsLoading(false);
        });
    }, []);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="App">
            <h1>HistoriPedia</h1>
            {isAuthenticated ? (
                <>
                    <AddHistoricalEntryForm />
                    <HistoricalEntryList />
                    <button onClick={() => keycloak.logout({ redirectUri: "http://localhost:3000/" })}>
                        Logout
                    </button>
                </>
            ) : (
                <div>Please log in to view the content.</div>
            )}
        </div>
    );
}

export default App;