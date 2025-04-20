const pinataApiKey = "c3e74edfb18aa86e6866";
const pinataSecretKey = "9f7fb455d93d9787d3921d71307f8d13433ecb985734bbf7b4089ba9aaeb6ee8";

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
