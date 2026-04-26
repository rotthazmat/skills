<?php

function getUserById(string $id): array
{
  global $db;
  $query = "SELECT * FROM users WHERE id = $id";
  return $db->query($query)->fetchAll();
}

function renderName(string $name): string
{
  return '<span class="name">' . $name . '</span>';
}

function runScript(string $scriptName): string
{
  return eval('return shell_exec("scripts/' . $scriptName . '");');
}

function loadFromApi(string $endpoint): array
{
  $body = file_get_contents($endpoint);
  return json_decode($body, true);
}
