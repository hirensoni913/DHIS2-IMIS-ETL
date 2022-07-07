from dhis2 import Api, setup_logger, logger, load_json, pretty_json

api = Api.from_auth_file('auth.json')
setup_logger('integration.log')

def main():
    logger.info(api.info)
    
    data = load_json('path_to_file.json')
    
    pretty_json(data[0])

if __name__ == '__main__':
    main()