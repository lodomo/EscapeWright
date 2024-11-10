import yaml from 'js-yaml';
import fs from 'fs';

// Define a partial interface with only the fields you need
interface ApiConfig {
  api: {
    host: string;
    port: number;
  };
}

// Read and parse the YAML file
const file = fs.readFileSync('config.yaml', 'utf8');
const config = yaml.load(file) as Partial<ApiConfig>; // Partial type assertion here
let api_url: string = "";


// Safely access api host and port if they exist
if (config.api?.host && config.api?.port) {
  api_url = `http://${config.api.host}:${config.api.port}`;
  console.log(api_url); // Output the API URL
} else {
  throw new Error("Host or port information is missing in the config file.");
}

export { api_url };
