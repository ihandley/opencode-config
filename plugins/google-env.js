import { execSync } from "node:child_process"

function getSecret(name) {
  try {
    return execSync(
      `security find-generic-password -a "$USER" -s ${name} -w`,
      { encoding: "utf-8" }
    ).trim()
  } catch {
    return ""
  }
}

export const GoogleEnvPlugin = async () => {
  const clientId = getSecret("GOOGLE_OAUTH_CLIENT_ID")
  const clientSecret = getSecret("GOOGLE_OAUTH_CLIENT_SECRET")

  return {
    "shell.env": async (_, output) => {
      output.env.GOOGLE_CLIENT_ID = clientId
      output.env.GOOGLE_CLIENT_SECRET = clientSecret
    },
  }
}