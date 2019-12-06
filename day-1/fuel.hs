calculateFuelRequired :: [Integer] -> Integer
calculateFuelRequired = foldl addTillZeroFuel 0
   where
      addTillZeroFuel s m
         | fuel <= 7 = s + fuel
         | otherwise = addTillZeroFuel (s+fuel) fuel
         where fuel = (m `div` 3) - 2

main = interact (show . calculateFuelRequired . map (\m -> (read m :: Integer)) . lines)
