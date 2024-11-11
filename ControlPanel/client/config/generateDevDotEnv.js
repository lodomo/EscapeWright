// config/generateDotEnv.js
import { load } from 'js-yaml';
import { readFileSync, writeFileSync } from 'fs';

// Load the YAML file from the config directory
const yamlPath = "./config/config.yaml";
const fileContents = readFileSync(yamlPath, 'utf8');
const config = load(fileContents);

// Construct the API URL
const apiUrl = `http://localhost:${config.api.port}`;

// Define the path for the .env file in the project root
const envPath = "./.env";

// Write the API URL to the .env file
writeFileSync(envPath, `VITE_API_URL=${apiUrl}\n`);

console.log(`.env file generated with API_URL=${apiUrl}`);
