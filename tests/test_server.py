from escapewright import escapiserver

def main():
    server = escapiserver.EscapiServer("Test Server")
    server.run()

if __name__ == "__main__":
    main()