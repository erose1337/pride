import os
from pride.crypto.utilities import bytes_to_integer, integer_to_bytes

# Bit Sizes: 128, 256, 4096
Q_128=0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff43
P_128=0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff42fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc34000000000000000000000000000000000000000000000000000000000002cd9d
G_128=0xf87cd50ad9a72132467a3a876dcfc3dadd666dc45661ea954d0c329504ea8810de7aeec656d82e9c10f31cb67a971afb48948095f37dad9b8394cbe1958e270e86bbe64b00e37a6f52a838df11ccba875d066c81e58bace3303f4fbe2085a770317914b9a7830c605b6efb83cc8ce1089ef974f56eba341e3e0bb1eaf863136620250a3279fc44188078185e4d3fb14c2aadfb63c3ea255518faf31c010cc6eaa155f14f5f6369f03aac64573734a6bce77dd162bd631a4c36b34281fb4efb8e3d8dfdaa672c32b207648edc8d39b7c268200c73fc9a81439dee8c7292c5db41869c39e772b83e617c333d3da12b64de756721c227c63d21b7cbd3ab5b113778a8fe0625a779757d4a29e78a97eb58651d52d4eb8561f647b43fb055e50fc4b4af63509393ad92ce2049908cab2e5074e831f43a02565bf9893f981a57b00b6ec5c0e082ffd5f4f730dd2daf6fb883afd907679a8df7898bc6f5da57102dfe4faf457dd73ee5057190fa6f2bc007fa19f0601143e1217fe5ebbdfd632c4240ab59a28f1a9f0f4165856e9a950cc99d60fbcfc3d3c1ad79ea52b2584a46b274120222116f797d0b3545d7b8ecc8e63a02864fc7c0d120b91ff665fc0e6736f7bca040b733b1205c5f09e503ac14e1d35e4b53d93e1dafef22a14f209e6d3959998ec585b796a18b023651dd567da8f9b888c7d0c43abd1de6db013381789f9336
system_parameters_128 = (Q_128, P_128, G_128)
# log2(P) = 4096
# log2(Q) = 256
# log2(G) = 4096

#Bit Sizes: 256, 512, 16383
Q_256=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdc7
P_256=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdc6fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff22e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001eb7c3
G_256=0x5d40a528f9fdc9dc036aab4f43f0be9f1cac4da701e4ad212eae3fff9d503c92c8f6e49a936e66d7fb96fe0e37fc240e003a0d67cd3728045a9501a2b96eba2ac93f5bddb87b3fa9ecbca9fd8cec9811f6c7385fa053440a3bebb1c6e804a40dde79a12d884221e7b399371127562b054ca0bf666bada59824be7f3e8b3213e8bd5d5580142b76a45ecfedccc8db9b58974a572303517ac1fca83737d4af42de02bde3b154cc971f5d08c7272801ca78107b04c6ba1f8e557bbd34446ad3448c91b3a615d81fd2bf428749b34ae0fd184fc51031ea6620234ba4eb808f3913de7c821cd4355a0910149fe6abaab57b51a0779c7da8088dabc402bbd97601d82e1e9951170481392cc711d2952b122efc3c7c0a70834d1064a3f10946f0bf40e9696284c44f01519c7471ca27f1079f21c382e27533d3a1b2726eb55462004ee6838c92bcf6b45fb570bf1977d85c219850b97d4af07442e50f6983153b472b3b79ca88dbe96ff6952e75461c6f57705b7c740df3fd3264ae0f13cddcfdd4a9082899e0442ff9062599673261bfdba930e56da43dc5f8c0c0df126ed46d93f660df91a933b581f128c9778494c9d0b07463e290d1a9e9ad9e3d67e02a75435687bce1bc1f5d7a7ae6a1be763025a1081833fd311c5cb83bf93c4cbe931c1993b741f5ac50257bf38e41c852bd1825a40b50ddf4cdec296a40e8f94d37295d0255a28ba5fb2069b69a632ced861d1a885845699ddfa638d5302bf569e667c1f351d0e6d0b1cbc87edeb0ed94988b1ca946726f11e9a952c5e85be509b5ad379edf4c9826cf300308caff7326ad35564a8fb27a97867a6454d40a09c7a37fe325d6613a4b95933a3f0640b696d1d7fd804d5f677141c52092f1b8d1ec52c2f1dd85fc0d5ccd84db590736c4093a96e9a55503f0c0aace7997ee02f105a2ca63cec343d5878a1f4784c82843854c446ff52dcffb76ec81a2ef7bc704a2ea2cd31782de0f632a25df2dc20233426c9a7ce835a4fadd77211c5e3b3f4d35b195ec41b05962837b0195270873c9f8aa8f37347f9b3126416c730c2580613ffbe28588caa5295fd54267ae4cf9debd0bfcfe7059f19c39413d0bb48b3361b86c14cd13bdee19227fa7fac5b6cebdea93d7d75c7b58eeb85d59c137034faae2ee2b650c71b33183fdc8d4297f52883dbfbfdfe2fd4e9351af93b7c69049d46ff29686a50a68eb2fbf2ccdad5b48a3393ce87d9237bd69d7f6c3d5d220cf0307b3d1d3b0c445906b80002255ac89465865d69d9fb941af187f6ea6d4fd48edb12545dc1e2ea2f0e6b278591a5d723cc228f1a447447c85f3abbbbade72a0e88336defc72063c82b310991a61d76dd1938125391301d474e7253a53450b5e35a7dfc2b41504e61fea6cc9b514aea583770f45bf33cddde8854804ed2f5c9b46c5c79e551147f23c1e65196e8bac3678486e4f6127ac3043da6df329e48986c5b4c5a9baed7e8014b302c2fe3aa1d733a963accef0b29a6deda855c3f9f3344a9ecde8c96d8821d7c45e888fde118de1619f2836691e13179f011bae2ca4743f0b3dea0728b7c05fd3a051f9fb3cd4592908e85b5442247b5c0365d65ef196e0017db1eae92adb7616c292e4e1fc3e4781949cb90b1cf13d3d19195fbfd485160f57df5bf6d0bd81b896db084c06b4e6f911d7f8ea3c58e761d7e152451d5126548d9ce1572dfb865dac75ed22305558d42ecb4f0ee290ec271d669a12aca2649a7abc36850eb90d624f708aee705617060fea08f6507905edc3522d4702a0c7e9814cf339a4718387749b6c011f32f625c41de46eebb5dad4336fd07c2d0784b12522556ebdb196acc5902e7b3d4f7d22643f5cd520f44ffdbe15c98e0657595eaec3a4b73177becddf43b8eba0eddd447f8325e325f960e5beba5380fd4769ba272d2c39ea7843352059f3a14c5f5c86b734154d1bbdc1d175bda325bd533c846a8a2a9628203d769d82b80f90daad0f2a741e20ae74d6addd9e24bab4dd10a09641de39eecaa368620dd2e2017cf5a57363f3448a13ea370dd6a2a9c37fe4014fc4c8a075c4d4f4489dce6fe935829776179c451831430b1ebeac32ce9cb5cfe4bc7df148a5be1318344ee9ff7bf608264ce7495e69f4535ac32747c001c69f23cd4ab1d0de70e04f41d0ec126444c13fe1871d8bd6d0b69511d7ee6dc3cbcb6e037661ac069148d3a137a6bf3593a6984b30e9d6573454313f062940c187dfa83c18b511b1a032ba51ce788d4bfcc4d05c996e8486687802d3307b242f2a9f4770fa78fd8018430b9582311ce235f1e2bb5e4dcdc171d8c72814c7fa12eff6083c45dcb56ff7820293bb521552edf3ec0180abb2414244fafb0bd7fc92461ba6ed27df8aecc80f45057fa70e33f4eae1ed152a628282683b6f255f8be2ef546f25a1e8e832443bad10daf9a7706f61d914e088d9a84f42f4390258700731949450eed12954fc2c121e70a2fd63a207368e885e7f3a58511146cc6aaf3e0b0604c6ab66f05c3c669325d03e1824d85b94fa3ff982171928a0fd0319cdc1f5ae2dd2086e8e975e8ca3fe34a2bd2ea9041a0b767144f8657f9535131807432289abb8828a91100a78c8dab5a84b8996dbbd9670cf17282828373bbdfcfebef22ed6511ed815d6bd2fdea2cc56f22ee3c7d9629a86f71e21808a82cb04842d8e78bbeed67286e839a949c4b2031670e49924ddd5a10b941dda6f28e765f6e38855c7195b8e3843d2ae1d7c3b7a73370990ab6477fc45f46bdeeea9e5a456233dc2bb65286f1f5ee7ac0cb54142148fe228169c1555eb8fb5b332bacc476d87d2acf8f57a0ac472bdd95523e74fb1f47753d7d3dc66d60eddd7b7ff30337cb3d0621288b48805
system_parameters_256 = (Q_256, P_256, G_256)

#log2(P) = 16384
#log2(Q) = 512
#log2(G) = 16383

#Bit Sizes: 320, 640, 32768
Q_320=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffecf
P_320=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeceffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffbfba00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004c9367
G_320=0x21833d0680ae72b6a89e4a1ad8d39b93c52588915eb262a806ca963186ce1b8f36c0bfccf9f2b67f0e17a4051336fd72b50dcfc6b0c33b706f83583cfd7dbd934b0ec6f83749e350daa864c9cf91702fe3cb096720a99db93f4c794f5f96502dad3de0da733433052a92298765a54c8930f9034686156ac712580a564c9e6873e1d224bec15c16274217d82a2bd74555760606b62fa8c8d7a5c909a9bcf64507675f4bb46d2b4f19622ac1f52deb233403632ddea6eaf11a9b1a1d21f3e55fb2c58712a50320179e470d9c94f5dab6638f1b571930ca66d4caa63eebb11a43473c394ce9232797b5b5750f77894c37942fb517d91b03708c4c237e1b9c0cc5b3251af532f42d5b3a41455525a8ae66ffbc5af51739b9ab96a109c1c2deeecbe37093b5c86a876b828285aaf8a552bd915b5a91e991884ce46865412535720f929ba4ba0f7bdda8db17cfd4011ec382bdf056fbcbc5322f904e59e737bd5b01a8d4d58da8d226e719b7c574cee196e0ea4e07bbf1a99b315e339fd1bf04a9163d58ff3fd3a89ab515c1d12b04d8fd89db9d62d523dcc521a9cf9030cdde0d487bdc0200af2631b445c55fd1a38b04ec39c99d3258a9da5f992f2562231394ac7ee6ad31702a6f31e81f084387880bb2ce46f91ab1ac120b6e2a289f2f49f4677f571f2ee2df322fa1f0b6239d3586744dfb6b78d9cf5d0d1fbe3369defa0d7763388ff95f85e785b14ae8187ddefd1774a977c7a427abaae181fcad03d6f4bf78ed78910921b9df4a2bc9e64da1e1a93741e0ebfe2ad074b7725713c8018f2fe1720b49fd8bb8199f006ffbe343f7769bb34692a041caae45f5553735834063a8837c2ea274f52848ac983a8b995925c8f8b43c39b7858c6c8c04aef102825896aecda181e85534810b4f7597fcb3c7be9d69f6b2c91f329bb1d971aba9f4c6cac5a1ea8759f429fddc5a35ec3de5709efc0a7ee650059bd66152248dee1ff5bde932d04c0357123c8abf598f8f157064e463c0a9dec3b3dde0d9217ffadde49522af5b9df220c8d9fbb249664d3995e64365ae88cfaafe56cbbcca379276ae49cf2ef1c8c0be561152bb7d524cbe2b064e4e3451df26fb1167e1f2c717340651b7f653966e0dd7cae95e29ae64e5de05a9dcc4429311eca73c951850b0e198be47512d5fd699f20e47858effb184057c46c936eba21de60e3e0d48bebfb91c6d49887ea463a28d178a359c051a107f7ef17db14ee7f6234008d2b1bf19e18eabe2367010445a0bea8a37d021734c677ffb351253e0d41312f44d5011b6970ddd5a8a071349065394dfc0358db6ee0b6ca95f74c3bf6605123affba077482a1dc3a328e6e31aaaf5b19b58f99612b6a8561216b2724451af4f038e7dd4839af69740bdd5ef626df48bd78ec560a0129688bb5df854883a7d1020c0baaa1e9deda634082140fe0665ca14cbfa000cf5ff696d813ea406478b469acb163efda91bdf19d33ef7a67c2e906b2d4c1beffc60fb5f6904ec282d764bfa902410b9b6833e1159f33219b0a6282dfe3063c6c082e78e39332fbda0cfedbe93b64a89ce1c6755bc421514cf42112bd1010e815b99f18dc3c6372c8ed195324f573136a2506b2db31cedb2d29846d7063ed798d95bb65f71c9e6a771f1b4c61db28b2713bfc10f3c1571a5067f6b645fdcc50969975801ada0f149e2f19837127ec030cf4a0afc5e53338a0c099e5ad57693949f8e7b7c8660a2e0cba8706ce672099ecb47b218df6920a38a989b942848a1d890cab7ed1e98e928f16f3b392e91f1b4fe310c3710c7dc56c5644d970028eeed3eacf25c399f6049d0f90cc8a42796d6083a91bb771d0fd95deba37c7ccb92ce97ddf44325d9a234248df372ab02e4de42febe9c7b20fba5e3ba05ebb549faaf5d559d9ccf8f535fa75626147e9f10d1b9d9b675713abc3a6554b885a7b2a6075bc8e511e35c80879479245641c69b6a74c8c2de14ba0d10b1d87d27816e45b1dc40e4d35be614de737b414cc2b164ccea35fbe36dcb5de44a87033ea4f855476ca83336a0a654c28439350e9afd45cc639645969b49825d30256b55d3f24405bebe630d42a07a19225a0ca1b39fcddd7e72bdd7a222dae3ec9067ce4b7dd5f16ac9a11fe194ea656c933dfa44438eb4365f6c6c499e7863891dd2a3c10812abeebcf278d369d39577a20dbb7661f1f52227ddf47d6ba350d6a08e45c4714fd46d98505aed51a28dd2f5c2b17193e008f49f2e6d1a19b3824a372de971dee84415f71c959ea7a414c17d4f55858575235a83aee67126e98f978c5a7644349e07ba4401eaf890f9d8169f058920fba74ca0435d35914302cbdf3217528a376b4cc5118e802bb726ad9c5a9182e1d008c30848bece9d6b56997b1ff0dae52a197723a9efd250b5a530b9e72190d325f9b391d062e5ff2a2b4d4269829a93baabcfe7e477710863b543570ac7755acd893cc04853317db1fe5cc39a9554bd54dc876ef9377742eb0b8d1ecb07997f83b3cddf1f54a7f9f1ed59989f143e0d5028817702e84a2589c945bb957657e37ccb5450776c0805a4059c9515d81cbed841c920b0394e2cb8917f57e94bb0a40d5b823126790e64e96efb2d3aba8ea0f0b4a147148bfd9c86b336d3e98020fe80f016a69cce7cb63bcfc6040ff9e777e15c7b83adf3ef32f27d4e553e55ff2e61de3dca52779368413d7ab4b76b5b78134a0ed520f79b3413a1580f2424d430553deaccc2966f7f2b031891e38de4302a4887af6a8a34674a07cedac0f6d7fb50f837b6be7809e4cefed375a82c9a9d27c8ba434de5e1a503ea35452ba19723846e500abd925b646f23675d2f70078785db4d7b0d65c3dfe3c5a5e160eb408f39c57289ee5bdbdab72507c176b44f51d5578df0ec0ad71e426b10bd8ad3bfaee8c475c09d241b0ccd64c967fe2d7a19e0df888c856425e791aba7cb2abf3faec2b3013780f3cc57fd228bc8336dbdd20d7982a5764e49e4f7a45249c46e4631a20e614755e4e8d1851ae60b7fa5016e923aa83fad509e38aec2d2ab31e887d47080b0c0a992d87b22ace37649bf0f025077110c7b0ff9570049883bf978aa1f362442ecfa31463707dc466e942313055c352b7d58b1b93fd3da05357289b2566d8d29a066b86057b2c4d7b2ba31f73d1ac2ed7aa7fed4037afab6fdbb358087b2ef2c47af9fbf335358612a6ada035199cb50b0017ce228df472d09fe69a273805a6ea60cba5f087d61cb99e05efc3af039cc94860590bf7dd908d6540ff88f36a33c1fb3be586519dc071ddbb467865ac8160e043123f486ce57c6aa770b5438c899de3c76661c9fefdf978a0e09b5c3525596247473d5248e9f99605fc35fb37cfe70ea55f5d64055981e739a3c5aed358f958b0226cd7b1a28c0c2f5239770862a016d495022ca64fe4d1cac92307c3f7cdf2cfec73696c835e1cd880034051157463c95a836fbecd12753a570c16583f845363980e09781c4a9151fc5b12aebc14baf645400f2979613f8542403fcedde3a14ef281b06a6a54cbbb79485ea636b9ecc814a2971506ee27049f00386ac191a16711da6175d454d9b7b0207af9ea5f46eae32eb3b92788a8ba9851ba74b12189f6492b640904bc266b02ebf3d2f310e15d4942da57412532a2ef1214b7ac207ebadeb3c24b764475be7a771a466f98cce84d2f13a676b65833c47220cfbe561a6e99aefcf10d95c0ca4dc983b4d408af77fd5326a855c3d06747d90511da54728277b1ce3f3b52d95419f3a930a0a65be13d2cad174e42cd3670ece1b9d5d086d951edc6275706ad4f19973ca61478cec5de9d5592bdf7172875fbac1eb759b13f7c5ce3d1a366b1a8fd8cc74b6fb4734d7cfa63c6a91ed4026eaa27df6544c7617119fce6d59808ffe024df9af731cd946e80fd5da21781a2744fcaeefe4963f48834447ee0eacce86d7adacbfef58935e0796c569c809a392a5ac1c90416ea2de6c6ddbe3893b9eb9375b41b0e785706601d1f3d4fded39121e552102d1f6cd2cc3e03419fb3be949b2429b28f82201bfa963f8e86731f33590691910c13ea51b1f8f45e53ca42b1d7dacd72943c214422f68861b45991d8b02d6efde540b2a9f36bede6a101964b3ad1ddb7789fd941065e784d0a74501e28b4c583887337f5200a99df3cbb459f4b9d39aff4aef952a734e2d952d6db09ff168d95b03694638c78f69485c2fbdd094b6e08ba5dae05fd82f2bba23489636a021822906d59b0541d5685e8713cd81469ea129fefe533b3ce91f2c80c163db9421e524f54dee8601fbd30a2b736e01a6ad58f4a02394456fdfd33bf0d599f3ee791eefbe77a19e07e8b46ea1228f3f05c3a1b2d4b57328bfb99bcd3980a109dc6042287770a04f2c6f86bb42007d4dff78f21d6b86144073583e86555dc6971c42b8d2163b9aa9d31be1687f7e93afde28cfc5023c85bc9c32d3c18b9badaed2c6436c3e25c49f348e5aa52ea2fc76e577095f4367e270547efdf5e64585b41823eea724e5ac7402ac0452d7043bf471aa0dc9bb0381223e3a8d5d9991b9762c640992a99b294619e561031cd4b286d66069160bd56e1673e62a60cd0348e98dcdba7d8fcadc362d04e6b92813701fbd8751f9effd63c470fcfb163aae25b05b5bab28129297b6370c788e64454bcc8c6b179d8014a324c3ffb5c75c4d4804d26b85ab839cbec89c7b23cdf96483507decc1f988063de0759d7111e144b440b0a78df4fd5bf07f4c31cf04c541a8ec9eda05132bd147f3a4807fc3fabbe9e63e57db7d54ef63fc09dbc542c2f93f6079f80279f157f046ccf553d45bca8c114327604bb29de09b7212f661518a750cf7a9ca074d751c881f4a9363356a9544edb6dcb78e89c358dc247495baf99af632010e2a08a47d7189aca3ed8fe4b6551850aaa21335751bcdfe2bc1b6400587788216fde9181161f7544c76e8bb0f869c587047c7b1d3d7cee121aa324cfcd9e54f79cbb236765aa21a81f3d1928650d0ffe622651ccfa4013e919216eccb7803736f8b288269e2eab53e491dd499cc4c9d90d37748f3685057ea449066508d285c79dd753d5df61d37402b33089198f534cbe575d9206d0e6b7dd191186994af71c2744d3c42440a3b00f8a55d0102916ce3144e7e22a2d46dc5888893440e25e0c8e97da31bb5a12b24f9af5f31330ab96d348f035359d39619c943d0b8ac74d913e015e1139f46bb29012736bed9f7263f961677b043934e50ce138d33be43f40f24e028cf543fd6e2867820eb025f8014f9c9eed86fc5fab492cfc3f8ec0bf368d6a8eb6387868b7b6d6cbda9f297ba0efe3d03c1848db4a45b1d92ae28cbf82ac669f1825e4da7ff32dbea978e25229b4553c8ab37f24c9d0e91ed330ded5c43213d04b5615c01a6650b81b258e40d1c9eb2762d48161fb40dc633d9556d102f424f3c5152f3372795c950f54dfa5fbdc7b627ffe721cc71ae0e3807b2a7c0ba1abe39fd1029b5d4f0c4a849d7b9979f54fdcb5925f6ecda5ba8a6bd82a81c111808fddc961223326da469835a5134ff316156ce4d17ee5f535e9e3bd2d3f66ef64d4c5bcb98d1df72d5d4dde0c9fa2701371043968142ea39dac84e315ae76ae213462be63094b4e8fb6d07b1b430752c50e72e5be06c96a931a5511d76377381d3e5280ae4310541bdf174655d3c929bcd2e7f3beba5d41e17758d06a6f65ce0a9957c668cb30b797a4acf8fbd79d530408e52fbd4e2e00f8a2ad5f92bb387db332c532
system_parameters_320 = (Q_320, P_320, G_320)
#log2(P) = 32768
#log2(Q) = 640
#log2(G) = 32766

random_number = lambda size : bytes_to_integer(bytearray(os.urandom(size)))

def random_number(q):
    in_bytes = integer_to_bytes(q)
    key = bytearray(os.urandom(len(in_bytes)))
    key_int = bytes_to_integer(key)
    while key_int > q:
        key.pop(-1)
        key_int = bytes_to_integer(key)
    return key_int
   
def generate_key(q):    
    key = random_number(q)
    assert 1 < key < q
    return key
    
def generate_private_key(q):
    return generate_key(q)
    
def generate_public_key(g, private_key, p):
    return pow(g, private_key, p)
    
def generate_token(public_b, private_a, key_a, p):
    return pow(public_b, private_a * key_a, p)
    
def generate_shared_secret(token_b, key_a, p):
    return pow(token_b, key_a, p)
    
def generate_keypair(q=Q_128, p=P_128, g=G_128):
    private_key = generate_private_key(q)
    return (private_key, generate_public_key(g, private_key, p))
        
def initiate_key_exchange(q=Q_128, p=P_128, g=G_128):
    return generate_key(q) 
    
def advance_key_exchange(public_key_b, private_a, key_a, p=P_128):
    return generate_token(public_key_b, private_a, key_a, p)
        
def finish_key_exchange(token_b, key_a, p=P_128):
    return generate_shared_secret(token_b, key_a, p)
                
def test_authenticated_key_exchange():
    key_a = generate_key(Q_128)
    private_a = generate_private_key(Q_128)
    public_a = generate_public_key(G_128, private_a, P_128)
    
    key_b = generate_key(Q_128)
    private_b = generate_private_key(Q_128)
    public_b = generate_public_key(G_128, private_b, P_128)
    
    token_a = generate_token(public_b, private_a, key_a, P_128)
    token_b = generate_token(public_a, private_b, key_b, P_128)
    
    secret1 = generate_shared_secret(token_b, key_a, P_128)
    secret2 = generate_shared_secret(token_a, key_b, P_128)
    assert secret1 == secret2
    
def test_initiate_advance_finish():
    for size in (128, 256, 320):        
        q, p, g = parameters = globals()["system_parameters_{}".format(size)]
        private_a, public_a = generate_keypair(*parameters)
        private_b, public_b = generate_keypair(*parameters)
        
        key_a = initiate_key_exchange(*parameters)    
        key_b = initiate_key_exchange(*parameters)
                
        token_a = advance_key_exchange(public_b, private_a, key_a, p)
        token_b = advance_key_exchange(public_a, private_b, key_b, p)
        
        secret1 = finish_key_exchange(token_b, key_a, p)
        secret2 = finish_key_exchange(token_a, key_b, p)
        assert secret1 == secret2
    
if __name__ == "__main__":
    test_authenticated_key_exchange()
    test_initiate_advance_finish()
    