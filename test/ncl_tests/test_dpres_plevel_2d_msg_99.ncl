begin
	plev = todouble((/ 1000,950,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,175,150,125,100, 80, 70, 60, 50,40, 30, 25, 20, 10 /))

	plev = plev * 100

	print(plev)

	ptop = min(plev)

	print(ptop)

	tmp_psfc = todouble((/1018,1016,1014,1012/))
	tmp_psfc = tmp_psfc * 100
	psfc = reshape(tmp_psfc, (/ 2,2 /))

	msg_fort = todouble(-99)
	psfc(0,1) = msg_fort

	psfc@_FillValue = msg_fort

	print(psfc)

	iopt = 0

	dp = dpres_plevel(plev, psfc, ptop, iopt)

	print(dp)
end
