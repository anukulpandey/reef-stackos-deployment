
# REEF StackOS Integration

In this dApp you can generate a free REEF account, claim that address & send testnet tokens from that account to another. 

Basically this website is just an API which can be integrated with other websites. At the moment it just returns json data.
## API Reference

#### Landing Page

```http
  GET /
```
shows the landing page & a message

#### Free wallet

```http
  GET /claim
```
you will be able to claim a free wallet address on reef chain [testnet + mainnet]

#### Send Tokens
```http
  GET /send/<address>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `address`      | `string` | **Required** address in which you want to send tokens |

#### Send Tokens
```http
  GET /fetch
```
fetches the account details


## Deployment

Docker Image URL

```bash
  https://hub.docker.com/repository/docker/0xbandar/stackos
```

