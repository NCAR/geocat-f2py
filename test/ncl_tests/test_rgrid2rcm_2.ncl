	; comparative test case in ncl_stable for missing values
begin

	random_setallseed(1234567890, 123456789) ; set random seeds to default values for repeatability;

	lat2d = (/(/ 1, 3, 5, 7/), (/1, 3, 5, 7/), (/1, 3, 5, 7/)/)
	lon2d = (/(/ 2, 2, 2, 2/), (/4, 4, 4, 4/),(/6, 6, 6, 6/)/)

	fi = random_normal(1, 1, (/2, 4, 3/)) ; 24 point data volume normal distribution about 1 with standard deviation of 1
	; fi_int = (/1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24/)
	; fi = reshape(fi_int, (/ 2, 3, 4 /))

	fi@_FillValue = -99 ; Set the missing value message to -99

	lat = (/1.0, 3.0, 5.0, 7.0/)
	lon = (/2.0, 4.0, 6.0/)

	fo = rgrid2rcm(lat, lon, fi, lat2d, lon2d, 0)

	; set missing values to -99 (default missing value)
    fi_msg = fi
	fi_msg(0,0,0)=-99
    fi_msg(0,2,2)=-99

	fo_msg = rgrid2rcm(lat, lon, fi_msg, lat2d, lon2d, 0)

	print(lat2d)
    print(lon2d)
    print(fi)
	print(fi_msg)
    print(lat)
    print(lon)
    print(fo)
	print(fo_msg)

end
