defmodule FourHorsemenTest do
  use ExUnit.Case
  doctest FourHorsemen

  test "greets the world" do
    assert FourHorsemen.hello() == :world
  end
end
