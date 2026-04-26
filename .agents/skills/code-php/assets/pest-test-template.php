<?php

declare(strict_types=1);

use Brain\Monkey\Functions;
use Mockery;

beforeEach(function () {
  \Brain\Monkey\setUp();
});

afterEach(function () {
  \Brain\Monkey\tearDown();
  Mockery::close();
});

test('does the expected thing', function () {
  $result = (new ExampleService())->execute('input');

  expect($result)->toBe('expected');
});

test('handles the edge case', function () {
  $result = (new ExampleService())->execute('');

  expect($result)->toBeNull();
});
