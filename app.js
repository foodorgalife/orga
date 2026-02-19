const symbols = "!@#$%^&*()-_=+[]{};:,.?/";

function randomInt(max) {
  const arr = new Uint32Array(1);
  crypto.getRandomValues(arr);
  return arr[0] % max;
}

function generatePassword(length, includeSymbols) {
  if (length < 4) throw new Error("Length must be at least 4");
  let alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  if (includeSymbols) alphabet += symbols;

  let out = "";
  for (let i = 0; i < length; i += 1) {
    out += alphabet[randomInt(alphabet.length)];
  }
  return out;
}

async function hashText(text, algorithm) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest(algorithm, bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function sortObject(value) {
  if (Array.isArray(value)) return value.map(sortObject);
  if (value && typeof value === "object") {
    return Object.keys(value)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortObject(value[key]);
        return acc;
      }, {});
  }
  return value;
}

async function fileDigest(file) {
  const buffer = await file.arrayBuffer();
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

document.getElementById("pw-generate").addEventListener("click", () => {
  const length = Number(document.getElementById("pw-length").value);
  const includeSymbols = document.getElementById("pw-symbols").checked;
  const output = document.getElementById("pw-output");
  try {
    output.value = generatePassword(length, includeSymbols);
  } catch (err) {
    output.value = err.message;
  }
});

document.getElementById("pw-copy").addEventListener("click", async () => {
  const value = document.getElementById("pw-output").value;
  if (!value) return;
  await navigator.clipboard.writeText(value);
});

document.getElementById("hash-generate").addEventListener("click", async () => {
  const text = document.getElementById("hash-input").value;
  const algorithm = document.getElementById("hash-algo").value;
  const output = document.getElementById("hash-output");
  output.value = await hashText(text, algorithm);
});

document.getElementById("json-format").addEventListener("click", () => {
  const input = document.getElementById("json-input").value;
  const indent = Number(document.getElementById("json-indent").value);
  const sort = document.getElementById("json-sort").checked;
  const output = document.getElementById("json-output");
  const error = document.getElementById("json-error");

  try {
    let parsed = JSON.parse(input);
    if (sort) parsed = sortObject(parsed);
    output.value = JSON.stringify(parsed, null, indent);
    error.textContent = "";
  } catch (err) {
    output.value = "";
    error.textContent = `Invalid JSON: ${err.message}`;
  }
});

document.getElementById("dupes-check").addEventListener("click", async () => {
  const files = [...document.getElementById("dupes-files").files];
  const out = document.getElementById("dupes-output");
  if (!files.length) {
    out.textContent = "Please select files first.";
    return;
  }

  const buckets = new Map();
  for (const file of files) {
    const digest = await fileDigest(file);
    if (!buckets.has(digest)) buckets.set(digest, []);
    buckets.get(digest).push(file.name);
  }

  const groups = [...buckets.entries()].filter(([, names]) => names.length > 1);
  if (!groups.length) {
    out.textContent = "No duplicates found in selected files.";
    return;
  }

  out.textContent = groups
    .map(([digest, names], i) => `Group ${i + 1} (${digest.slice(0, 16)}...):\n- ${names.join("\n- ")}`)
    .join("\n\n");
});
