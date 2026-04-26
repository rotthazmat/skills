<?php

declare(strict_types=1);

namespace App\Services;

final class ExampleService
{
  public function __construct(
    private readonly DependencyInterface $dependency,
  ) {}

  public function execute(string $input): ?string
  {
    return null;
  }
}
