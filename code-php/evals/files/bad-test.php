<?php

use Brain\Monkey\Functions;
use Mockery;

beforeEach(function () {
  \Brain\Monkey\setUp();
  Functions\when('get_option')->justReturn('default');
});

afterEach(function () {
  \Brain\Monkey\tearDown();
  Mockery::close();
});

test('returns default when no option set', function () {
  $result = get_configured_value();
  expect($result)->toBe('default');
});

test('returns the stored option value', function () {
  Functions\expect('get_option')
    ->once()
    ->with('my_setting')
    ->andReturn('custom');

  $result = get_configured_value();
  expect($result)->toBe('custom');
});
