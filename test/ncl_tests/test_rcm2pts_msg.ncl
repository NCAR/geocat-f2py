begin
	tmp_fi = todouble( (/ 0.22244407, 0.21744122, -1.17592971, -0.045692, -0.82479881, 3.54210855, -2.62469226, -0.58759951, -0.09576288, 2.28897569, 1.22735336, -0.66038981, -1.84521102, -1.16090476, -1.74572171, 0.16554497 /) )
	
	fi = reshape(tmp_fi, (/ 1,4,4 /))

	fi@_FillValue = fi(0,0,0)

	tmp_lat2D= todouble( (/ 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3 /) )
	lat2D = reshape(tmp_lat2D,(/4,4/))

	tmp_lon2D = todouble( (/ 0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3/) )
	lon2D = reshape(tmp_lon2D,(/4,4/))

	lat1D = todouble( (/ 0,0.5,1.0,1.5,2.0,2.5,3.0/) )

	lon1D = todouble( (/ 0,0.5,1.0,1.5,2.0,2.5,3.0/) )

	opt = False
	opt@debug = True

	r = rcm2points(lat2D, lon2D, fi, lat1D, lon1D, 0)

	print(lat2D)
	print(lon2D)
	print(fi)
	print(lat1D)
	print(lon1D)
	print(r)
end
