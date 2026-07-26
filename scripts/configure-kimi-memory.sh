#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config_dir="${AKOS_CONFIG_DIR:-$HOME/.config/akos}"
secret_file="$config_dir/kimi-memory.env"
receipt_dir="${AKOS_RECEIPT_DIR:-$repo_root/.akos/receipts/kimi-memory}"

mkdir -p "$config_dir"
umask 077

read_secret() {
  local variable_name="$1"
  local prompt="$2"
  local current_value="${!variable_name:-}"
  if [[ -n "$current_value" ]]; then
    printf '%s' "$current_value"
    return
  fi

  local entered
  read -r -s -p "$prompt" entered
  printf '\n' >&2
  if [[ -z "$entered" ]]; then
    printf 'Required value was empty: %s\n' "$variable_name" >&2
    exit 2
  fi
  printf '%s' "$entered"
}

moonshot_key="$(read_secret MOONSHOT_API_KEY 'Moonshot/Kimi API key: ')"
memoryplugin_key="$(read_secret MEMORY_PLUGIN_API_KEY 'MemoryPlugin API key: ')"

tmp_file="$(mktemp "$config_dir/.kimi-memory.env.XXXXXX")"
cleanup() {
  rm -f "$tmp_file"
}
trap cleanup EXIT

{
  printf 'MOONSHOT_API_KEY=%q\n' "$moonshot_key"
  printf 'MEMORY_PLUGIN_API_KEY=%q\n' "$memoryplugin_key"
  printf 'MOONSHOT_BASE_URL=%q\n' 'https://api.moonshot.ai'
  printf 'MEMORY_PLUGIN_BASE_URL=%q\n' 'https://www.memoryplugin.com'
  printf 'KIMI_MODEL=%q\n' 'kimi-k3'
  printf 'AKOS_MEMORY_SOURCE=%q\n' 'akos-kimi'
  printf 'USER_TIMEZONE=%q\n' 'Pacific/Honolulu'
} > "$tmp_file"

chmod 600 "$tmp_file"
mv "$tmp_file" "$secret_file"
trap - EXIT

set -a
# shellcheck disable=SC1090
. "$secret_file"
set +a

cd "$repo_root"
python -m operational_cognition.connectors.live_memory \
  --receipt-dir "$receipt_dir" \
  probe

printf '\nCredential file: %s\n' "$secret_file"
printf 'Permissions: '
stat -f '%Sp' "$secret_file" 2>/dev/null || stat -c '%A' "$secret_file"
printf 'Provider receipt directory: %s\n' "$receipt_dir"
