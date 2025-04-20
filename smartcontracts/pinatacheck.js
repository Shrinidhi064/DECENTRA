const pinataApiKey = "";
const pinataSecretKey = "";

// Function to fetch all pinned files from Pinata
async function fetchPinataFiles() {
    try {
        const response = await fetch("https://api.pinata.cloud/data/pinList", {
            method: "GET",
            headers: {
                "pinata_api_key": pinataApiKey,
                "pinata_secret_api_key": pinataSecretKey
            }
        });

        if (!response.ok) {
            console.error("❌ Failed to fetch Pinata files:", response.statusText);
            return [];
        }

        const data = await response.json();
        return data.rows; // Returns list of pinned files
    } catch (error) {
        console.error("❌ Error fetching files from Pinata:", error);
        return [];
    }
}

// Function to check if 'prateek_agarwal_sign' is present
async function checkIfFileExists() {
    const files = await fetchPinataFiles();
    console.log(files)
    // Find if 'prateek_agarwal_sign' exists
    const match = files.find(file => file.metadata.name === "prateek_agarwal_sign.png");

    if (match) {
        console.log("✅ 'prateek_agarwal_sign' is present in Pinata!");
        console.log("CID:", match.ipfs_pin_hash);
        console.log("URL:", `https://gateway.pinata.cloud/ipfs/${match.ipfs_pin_hash}`);
    } else {
        console.log("❌ 'prateek_agarwal_sign' is NOT found in Pinata.");
    }
}

// Run the check
checkIfFileExists();
