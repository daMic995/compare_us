/**
 * Generates a unique user ID and assigns it to the session.
 * If the user ID already exists in Redis, it is returned.
 * @returns {Promise<string | null>} The user ID or null if an error occurred.
 */
const getUserId = async (): Promise<string | null> => {
    try {
        // Send a GET request to the server to generate a new user ID
        const response = await fetch('/api/python/generate_user_id', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Parse the JSON response
        const data = await response.json();

        // Return the user ID
        return data.user_id;
    }
    catch (error) {
        // Log any errors
        console.error(error);
        // Return null if an error occurred
        return null;
    }
};

export default getUserId