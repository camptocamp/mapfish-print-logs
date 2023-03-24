# MapFish Print logs

Micro service to provide customers access to the mutualize print's logs.

Authentication can be done through the `X-API-Key` HTTP header.

## Changelog

The `accounting.a4price` in the config is moved to the `PRINT_A4PRICE` in environment variables.

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```
